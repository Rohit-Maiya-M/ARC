from tree_sitter import Language, Parser
import tree_sitter_java

from app.indexing.models.code_symbol import CodeSymbol
from app.indexing.parsers.base_parser import BaseParser


class JavaParser(BaseParser):

    def __init__(self):
        self.parser = Parser(
            Language(tree_sitter_java.language())
        )

    def parse(self, content: str) -> list[CodeSymbol]:

        source = content.encode("utf-8")

        tree = self.parser.parse(source)

        symbols: list[CodeSymbol] = []

        context = {
            "type_stack": []
        }

        self._walk(
            tree.root_node,
            source,
            symbols,
            context
        )

        return symbols


    def _walk(
        self,
        node,
        source: bytes,
        symbols: list[CodeSymbol],
        context: dict,
    ):

        entered_type = False

        if node.type in (
            "class_declaration",
            "interface_declaration",
            "enum_declaration",
            "record_declaration",
        ):            

            identifier = self._find_child(node, "identifier")

            if identifier is not None:

                type_name = self._node_text(identifier, source)

                context["type_stack"].append(type_name)

                entered_type = True

            if node.type == "class_declaration":

                self._extract_class(
                    node,
                    source,
                    symbols,
                    context,
                )

            elif node.type == "interface_declaration":

                self._extract_interface(
                    node,
                    source,
                    symbols,
                    context,
                )

            elif node.type == "enum_declaration":

                self._extract_enum(
                    node,
                    source,
                    symbols,
                    context,
                )

            elif node.type == "record_declaration":

                self._extract_record(
                    node,
                    source,
                    symbols,
                    context,
                )

        elif node.type == "method_declaration":

            self._extract_method(
                node,
                source,
                symbols,
                context,
            )

        elif node.type == "constructor_declaration":

            self._extract_constructor(
                node,
                source,
                symbols,
                context,
            )

        for child in node.children:

            self._walk(
                child,
                source,
                symbols,
                context,
            )

        if entered_type:

            context["type_stack"].pop()

    def _find_child(self, node, node_type: str):

        for child in node.children:
            if child.type == node_type:
                return child

        return None


    def _node_text(self, node, source: bytes) -> str:

        return source[node.start_byte:node.end_byte].decode("utf-8")


    def _node_location(self, node) -> dict[str, int]:

        return {
            "start_line": node.start_point[0] + 1,
            "start_column": node.start_point[1],

            "end_line": node.end_point[0] + 1,
            "end_column": node.end_point[1],

            "start_byte": node.start_byte,
            "end_byte": node.end_byte,
        }


    def _extract_class(
        self,
        node,
        source: bytes,
        symbols: list[CodeSymbol],
        context: dict,
    ):        
        identifier = self._find_child(node, "identifier")

        if identifier is None:
            return

        class_name = self._node_text(identifier, source)

        location = self._node_location(node)

        symbol = CodeSymbol(
            language="java",

            symbol_name=class_name,

            symbol_type="class",

            symbol_path="/".join(context["type_stack"]),

            **location,

            content=self._node_text(node, source),
        )

        symbols.append(symbol)

    def _extract_method(
        self,
        node,
        source: bytes,
        symbols: list[CodeSymbol],
        context: dict,
    ):

        identifier = self._find_child(node, "identifier")

        if identifier is None:
            return

        method_name = self._node_text(identifier, source)

        location = self._node_location(node)

        symbol = CodeSymbol(
            language="java",

            symbol_name=method_name,

            symbol_type="method",

            symbol_path="/".join(
                context["type_stack"] + [method_name]
            ),

            **location,

            content=self._node_text(node, source),
        )

        symbols.append(symbol)


    def _extract_constructor(
        self,
        node,
        source: bytes,
        symbols: list[CodeSymbol],
        context: dict,
    ):

        identifier = self._find_child(node, "identifier")

        if identifier is None:
            return

        constructor_name = self._node_text(identifier, source)

        location = self._node_location(node)

        symbol = CodeSymbol(
            language="java",

            symbol_name=constructor_name,

            symbol_type="constructor",

            symbol_path="/".join(
                context["type_stack"] + [constructor_name]
            ),

            **location,

            content=self._node_text(node, source),
        )

        symbols.append(symbol)


    def _extract_interface(
        self,
        node,
        source: bytes,
        symbols: list[CodeSymbol],
        context: dict,
    ):

        identifier = self._find_child(node, "identifier")

        if identifier is None:
            return

        interface_name = self._node_text(identifier, source)

        location = self._node_location(node)

        symbol = CodeSymbol(
            language="java",

            symbol_name=interface_name,

            symbol_type="interface",

            symbol_path="/".join(context["type_stack"]),

            **location,

            content=self._node_text(node, source),
        )

        symbols.append(symbol)


    def _extract_enum(
        self,
        node,
        source: bytes,
        symbols: list[CodeSymbol],
        context: dict,
    ):

        identifier = self._find_child(node, "identifier")

        if identifier is None:
            return

        enum_name = self._node_text(identifier, source)

        location = self._node_location(node)

        symbol = CodeSymbol(
            language="java",

            symbol_name=enum_name,

            symbol_type="enum",

            symbol_path="/".join(context["type_stack"]),

            **location,

            content=self._node_text(node, source),
        )

        symbols.append(symbol)


    def _extract_record(
        self,
        node,
        source: bytes,
        symbols: list[CodeSymbol],
        context: dict,
    ):

        identifier = self._find_child(node, "identifier")

        if identifier is None:
            return

        record_name = self._node_text(identifier, source)

        location = self._node_location(node)

        symbol = CodeSymbol(
            language="java",

            symbol_name=record_name,

            symbol_type="record",

            symbol_path="/".join(context["type_stack"]),

            **location,

            content=self._node_text(node, source),
        )

        symbols.append(symbol)