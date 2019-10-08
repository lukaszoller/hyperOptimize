from src.hyperOptimizeApp.logic.EstimateTimeModel import EstimateTimeModel
from src.hyperOptimizeApp.logic.HyperParams import HyperParams

class OptimizeParamsModel:
    def __init__(self):
        self.hyperParams = HyperParams()

    def estimateTime(self):
        return EstimateTimeModel.estimateTime(hyperParams=self.hyperParams)

    def optimize(self):
        # Initialize model list

        # Initialize results table (len(hyperparams(1)*len(hyperparamy(2)*...)

        # Loop through all hyper params
        # 1. Learning rate
       for lr in range(0, len(self.hyperParams.learningRateArray)):
            # 2. Decay rate
            for decay in range(0, len(self.hyperParams.lrDecayArray)):
                # 3. Loss function
                for lossFunc in range(0, len(self.hyperParams.lossFunctionArray)):
                    # 4. Number of layers
                    for nbrLayers in range(0, len(self.hyperParams.nbrOfLayersArray)):
                        # 5. Number of nodes per layer
                        for nbrNodes in range(0, len(self.hyperParams.nbrOfNodesPerLayerArray)):
                            # 6. Dropout rate
                            for dropoutRate in range(0, len(self.hyperParams.dropoutRatePerArray)):


                        # Build model

                                # Train model
                                    # get time
                                    # train model
                                    # get time
                                # Test model
                                    # test model
                                    # add model to model list
                                    # add row with used params and results (error, training time) to result table


