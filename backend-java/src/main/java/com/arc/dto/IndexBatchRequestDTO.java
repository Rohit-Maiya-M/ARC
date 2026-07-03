package com.arc.dto;


import lombok.Builder;
import lombok.Data;

import java.util.List;

@Data
@Builder
public class IndexBatchRequestDTO {
    private List<IndexRequestDto> requests;
}
