#FixedTimeInterval
from fixed_length_individual import FixedLengthIndividual
import random
class FixedTimeIntervalGA:


	intervalNum = 0
	totalSimulationStep = 0
	timeSpan = 0
	individualNum = 10
	phaseNum = 4
	mutationRate = 0.1 
	offspringNum = 4
	minimumTimeForEachPhase = 0  #define the minimum time for each phase
	def __init__(self, intervalNum, totalSimulationStep, individualNum, offspringNum):
		self.intervalNum = intervalNum
		self.totalSimulationStep = totalSimulationStep 
		self.timeSpan = totalSimulationStep/ intervalNum
		self.offspringNum = offspringNum
		self.individualNum = individualNum
		self.individualList = []
		
	
	def getAverageFitness(self):
		totalFitness = 0.0;
		for i in xrange(len(self.individualList)):
			totalFitness = totalFitness + self.individualList[i].fitness
		return totalFitness / len(self.individualList)
			

	def generateIndividualList(self):
		for _ in xrange(self.individualNum):
			self.individualList.append(FixedLengthIndividual(self.timeSpan, self.intervalNum,
									 self.phaseNum, self.minimumTimeForEachPhase, self.mutationRate))



	def generateOffspring(self):
		offspringNum = self.offspringNum
		offspringList = []
		#each time generate two offspring, then we can divide it by 2
		offspringNum = offspringNum / 2
		for _ in xrange(offspringNum):
			firstIndex = random.randint(0, len(self.individualList) - 1)
			secondIndex = firstIndex
			while firstIndex == secondIndex:
				secondIndex = random.randint(0, len(self.individualList) - 1)

			firstClone = self.individualList[firstIndex].clone()
			secondClone = self.individualList[secondIndex].clone()

			firstClone.crossover(secondClone)

			offspringList.append(firstClone)
			offspringList.append(secondClone)

		self.addOffspringToIndividualList(offspringList)
		return offspringList

	def addOffspringToIndividualList(self, offspringList):
		for i in xrange(len(offspringList)):
			self.individualList.append(offspringList[i])


	def rank(self):
		self.individualList = sorted(self.individualList, key = lambda trafficInd : trafficInd.fitness, reverse = True)

	def select(self):
		selectNum = self.individualNum
		self.individualList = self.individualList[0 : selectNum]

	def mutate(self):
		#mutate all the parents and offsprings
		for i in xrange(len(self.individualList)):
			self.individualList[i].mutate()

	def evaluateAll(self):
		for i in xrange(len(self.individualList)):
			self.individualList[i].evaluate(self.totalSimulationStep)

	def getBestIndividual(self):
		return self.individualList[0]








