import traci

class Simulate:
    trafficLightIdList = ["65470359"]
    #trafficLightIdList = ["0/0"]
    trafficLightPhaseNumList = [4]
    subIntervalNum = 0
    timeScaleFactor = 1000
    
    
    def __init__(self, portNum, individual, subIntervalNum):
        """
        @param portNum the port that this class can use to evaluate the individuals, also the port num is used to identify a connection to the sumo server
        @param genes the traffic timeing for each traffic light
        """
        
        self.portNum = portNum
        self.individual = individual 
        self.subIntervalNum = subIntervalNum
    
    #using strategy design pattern to get fitness
    def beginEvaluate(self, totalSimulationStep, strategyStr = "arrivedNumOnly"):
        if strategyStr == "arrivedNumOnly" :
            return self.evaluateArrivedNumMinusTeleportNum(totalSimulationStep)
        elif strategyStr == "arrivedNumMinusWaitingTime":
                return self.evaluateArrivedNumMinusWaitingTime(1, 1)
            
    def evaluateArrivedNumMinusTeleportNum(self, totalSimulationStep):
        """
        Given the parameters during initialization, we run the simulator to get the fitness
        using port num to identify a connection
        """
        traci.init(self.portNum, 10, "localhost", str(self.portNum))

        totalNumPassed = 0
        intervalStep = totalSimulationStep / self.subIntervalNum
        stepIndex = 0
        prevIntervalIndex = -1
        for _ in xrange(totalSimulationStep):
            currentIntervalIndex  = stepIndex / intervalStep
            stepIndex = stepIndex + 1
            if currentIntervalIndex != prevIntervalIndex:
                self.changeTrafficLight(currentIntervalIndex)
            prevIntervalIndex = currentIntervalIndex
                
            traci.simulationStep()
            totalNumPassed = totalNumPassed + traci.simulation.getArrivedNumber()# - traci.simulation.getEndingTeleportNumber()
        traci.close()
        self.fitness = totalNumPassed
        return totalNumPassed
    
    
       
    def changeTrafficLight(self, timeIndex):
        currentTiming = []
        for i in xrange(len(self.individual.genes[timeIndex].timing)):
            currentTiming.append(self.individual.genes[timeIndex].timing[i] * self.timeScaleFactor)
        
        
        for i in xrange(len(self.trafficLightIdList)):
            tlsLogicList = traci.trafficlights.getCompleteRedYellowGreenDefinition(self.trafficLightIdList[i])
            tlsLogicList = tlsLogicList[0]
            phaseList = []
            for j in xrange(len(tlsLogicList._phases)):
                phaseList.append(traci.trafficlights.Phase(currentTiming[j], currentTiming[j], currentTiming[j], tlsLogicList._phases[j]._phaseDef))
            tlsLogicList._phases = phaseList
            traci.trafficlights.setCompleteRedYellowGreenDefinition(self.trafficLightIdList[i], tlsLogicList)
        
    
    
