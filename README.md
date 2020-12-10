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
**XGBoost with default parameter:** *0.6687*

**XGBoost with `'scale_pos_weight': 1, 'max_depth': 3, 'reg_lambda': 0, 'gamma': 0, 'learning_rate': 0.1` as the optimal parameter:** *0.6927*

