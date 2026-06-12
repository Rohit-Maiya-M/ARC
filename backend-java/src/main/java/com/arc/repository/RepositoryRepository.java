package com.arc.repository;

import com.arc.entity.RepositoryEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RepositoryRepository extends JpaRepository<RepositoryEntity, Long> {

}
