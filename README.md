docker build -t awesome-covid19-q2-xgmodel:`<version_number>` .

or build a version of your existing container.

## Local Test
### Training
docker run \   
    -v $(pwd)/synthetic_data/training:/data:ro \
    -v $(pwd)/output:/output:rw \
    -v $(pwd)/scratch:/scratch:rw \
    -v $(pwd)/model:/model:rw \
    `awesome-covid19-q2-xgmodel:v4` bash /app/train.sh

### Prediction
docker run \   
    -v $(pwd)/synthetic_data/training:/data:ro \
    -v $(pwd)/output:/output:rw \
    -v $(pwd)/scratch:/scratch:rw \
    -v $(pwd)/model:/model:rw \
    `awesome-covid19-q2-xgmodel:v4` bash /app/infer.sh


## Submission to Synapse
https://www.synapse.org/#!Synapse:syn21849255/wiki/602419


## Results


| AUC  | scale_pos_weight| max_dept | reg_lambda | gamma | learning_rate|
|----------- | ----------- | -----------  | ----------- | ----------- | -----------| 
| 0.6687 | default | default | default | default | default |
| 0.6927   | 1 |  3 |  0 | 0 | 0.1 |
| 0.6989   | 0.5 |  2 |  0 | 0 | 0.1 |
| 0.6861   | 2 |  2 |  0.01 | 0.25 | 0.25|