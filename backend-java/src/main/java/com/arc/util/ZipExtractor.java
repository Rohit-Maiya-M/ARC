package com.arc.util;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class ZipExtractor {

    public static void extractZip(
            Path zipFilePath,
            Path targetDirectory
    ) throws IOException
    {
        try(
            ZipInputStream zis = new ZipInputStream(
                    Files.newInputStream(
                            zipFilePath
                    )
            )
        ){
            ZipEntry zipEntry;

            while(
                    (zipEntry = zis.getNextEntry())
                            != null
            ){
                Path newPath =
                        targetDirectory.resolve(
                                zipEntry.getName()
                        );

                if (zipEntry.isDirectory()) {

                    Files.createDirectories(
                            newPath
                    );

                } else {

                    Files.createDirectories(
                            newPath.getParent()
                    );

                    Files.copy(
                            zis,
                            newPath,
                            StandardCopyOption.REPLACE_EXISTING
                    );
                }
            }
            zis.closeEntry();
        }
    }
}
