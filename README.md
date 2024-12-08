# ROS2 RAG Project

### Environment and Tooling
[docker-compose.yml](https://github.com/Bonyoze/ros2-rag-project/blob/main/docker-compose.yml)

![image](https://github.com/user-attachments/assets/fa2d56c3-b97c-4fd3-b255-93f9384b6fe1)

### ETL Pipeline
Ingested URLs
- https://github.com/ros2/ros2_documentation
- https://github.com/ros-navigation/docs.nav2.org.git
- https://github.com/moveit/moveit2_tutorials.git
- https://github.com/gazebosim/docs.git

Raw data fetched and stored in `mongodb` using `poetry poe run-digital-data-etl`.

Storing `4` documents using the sources listed above.

### Featurization Pipeline

Raw data cleaned, chunked and embedded into the vector db using `poetry poe run-feature-engineering-pipeline`.

Creating `68466` chunks (`1500` chunk size, `100` chunk overlap) from the collected raw data.

### Deploying the App
https://huggingface.co/spaces/Bonyoze/ros2-rag-project
