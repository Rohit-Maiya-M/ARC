package com.arc.models;


import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class RepositoryFile {

    private String fileName;

    private String relativePath;

    private String extension;

    private String content;

}
