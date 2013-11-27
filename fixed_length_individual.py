import random
from single_traffic_light import SingleTrafficLight
from simulate import Simulate
from sumo import SUMO
#this is the kind of individual that has a fixed length
class FixedLengthIndividual:

	timeSpan = 0
	fitness = -0x7FFFFFF
	maximumTime = 100
	minTime = 0
	minimumTimeForEachPhase = 0
	def __init__(self, timeSpan, spanNum, phaseNum, minimumTimeForEachPhase, mutationRate):
		self.timeSpan = timeSpan
		self.spanNum = spanNum
		self.phaseNum = phaseNum
		self.mutationRate = mutationRate
		self.mininumTimeFroEachPhase = minimumTimeForEachPhase
		self.genes = []

		for _ in xrange(spanNum):
# 			timeSeries = self.generateARandomTimeSeriesForTheTrafficLight(timeSpan, phaseNum, minimumTimeForEachPhase)
			timeSeries = SingleTrafficLight.generateTrafficLightWithUpperAndLowerBound(phaseNum, minimumTimeForEachPhase)
			self.genes.append(SingleTrafficLight(timeSeries))



	@classmethod
	def generateARandomTimeSeriesForTheTrafficLight(cls, timeSpan, phaseNum, minimumTimeForEachPhase):
		timeList = []
		for i in xrange(phaseNum):
			timeList.append(minimumTimeForEachPhase)

		timeLeft = timeSpan - phaseNum * minimumTimeForEachPhase

		#guarantee that each phase have the minimum time
		for i in xrange(phaseNum):
			randTime = random.randint(0, timeLeft)
			timeList[i] = timeList[i] + randTime
			timeLeft = timeLeft - randTime
			if timeLeft == 0:
				break

		if timeLeft > 0:
			index = random.randint(0, phaseNum - 1)
			timeList[index] = timeList[index] + timeLeft

		return timeList
	
		
			
		


	def crossover(self, anotherIndividual):
		selectedCrossoverPoint = random.randint(0, self.phaseNum - 1)
		for i in xrange(self.spanNum):
			if i > selectedCrossoverPoint:
				tempTrafficLight = self.genes[i]
				self.genes[i] = anotherIndividual.genes[i]
				anotherIndividual.genes[i] = tempTrafficLight
		
		self.invalidate()
		anotherIndividual.invalidate()

	def mutate(self):
		hasMutated = False
		for i in range(self.spanNum):
			shouldMutate = random.random()
			if shouldMutate < self.mutationRate:
				hasMutated = True
				self.genes[i].mutateWithoutConstraint()
		if hasMutated:
			self.invalidate()

	def clone(self):
		newInd = FixedLengthIndividual(self.timeSpan, self.spanNum, self.phaseNum, self.minimumTimeForEachPhase, self.mutationRate)
		newInd.genes = []
		for i in xrange(newInd.spanNum):
			newInd.genes.append(SingleTrafficLight(self.genes[i].timing))
		newInd.fitness = self.fitness
		return newInd

	def evaluate(self, totalSimulationStep):
		
		#fitness didn't change because of crossover and mutation
		if self.fitness > 0:
			return self.fitness
		#if the fitness is greater than 0, then we don't need to evaluate again
		dataDir = "sumo/SampleRoad/Caltrain/"
		#dataDir = "sumo/SampleRoad/FTSP/"
		subProcess = SUMO.startSimulator(dataDir + "test.sumocfg")
		ind = Simulate(8813, self, self.spanNum)
		self.fitness = ind.beginEvaluate(totalSimulationStep)
		subProcess.wait()
		return self.fitness
	
	def invalidate(self):
		self.fitness = -0x7FFFFFF




#verify the intuitive answer
# if __name__ == "__main__":
# 	timeSeries = [[25, 3, 37, 135], [117, 31, 46, 6], [167, 0, 1, 32], [58, 26, 109, 7]]
# 	genes = []
# 	for i in xrange(len(timeSeries)):
# 		genes.append(SingleTrafficLight(timeSeries[i]))
# 	individual = FixedTimeIntervalGA(4, simulationStep, 30, 10)
	
	


