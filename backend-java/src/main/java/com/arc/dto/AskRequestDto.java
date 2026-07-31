package com.arc.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import jakarta.validation.constraints.NotBlank;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AskRequestDto {

    @JsonProperty("repository_id")
    @NotBlank(message = "Repository UUID cannot be empty!")
    private String repositoryId;

    @NotBlank(message = "Question cannot be empty!")
    private String question;

}