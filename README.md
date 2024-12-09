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

Raw data from sources can be fetched and stored in `mongodb` using `poetry poe run-digital-data-etl`.

This stores `4` documents using the sources listed above.

### Featurization Pipeline

Raw data can be cleaned, chunked and embedded into the vector db using `poetry poe run-feature-engineering-pipeline`.

This creates `68466` chunks (`1500` chunk size, `100` chunk overlap) from the collected raw data.

### Deploying the App

Gradio app is setup to be ran via `poetry run python -m app` and can be utilized at `http://localhost:7860`

Example demo runs:

1.
![image](https://github.com/user-attachments/assets/18be93a0-e11e-4fc0-a84c-f4627c2835e2)
2.
![image](https://github.com/user-attachments/assets/991c7d26-df48-4a40-9ea5-5799a23346e3)
3.
![image](https://github.com/user-attachments/assets/433138f9-e2cd-4570-aae2-c4527f5ada03)
