package com.arc.dto;


import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
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
    private Long repositoryId;

    @NotBlank(message = "Question cannot be empty!")
    private String question;

}
