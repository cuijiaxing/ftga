import random
class SingleTrafficLight:
	minTime = 0
	maxTime = 100

	def __init__(self, timeForEachPhase):
		self.timing = timeForEachPhase


	def mutateWithoutConstraint(self):
		timeSeries = self.generateTrafficLightWithUpperAndLowerBound(len(self.timing), self.minTime)
		self.timing = timeSeries
			

	def mutate(self, firstMutationPosition = -1, secondMutationPosition = -1):
		#we choose the mutaion position ourselves
		if firstMutationPosition == -1 and secondMutationPosition == -1:
			firstMutationPosition = random.randint(0, len(self.timing) - 1)
			secondMutationPosition = firstMutationPosition
			while secondMutationPosition == firstMutationPosition:
				secondMutationPosition = random.randint(0, len(self.timing) - 1)

		#then we mutate between these two 	


		firstTime = self.timing[firstMutationPosition]
		secondTime = self.timing[secondMutationPosition]

		if firstTime > secondTime:
			minimum = secondTime
		else:
			minimum = firstTime

		shouldIncrease = random.randint(0, 1)


		#increase the first timing and decrease the second timing
		if shouldIncrease == 1:
			increment = random.randint(0, minimum)
			self.timing[firstMutationPosition] = self.timing[firstMutationPosition] + increment
			self.timing[secondMutationPosition] = self.timing[secondMutationPosition] - increment
		else:
			#decrease the first timing
			decrement = random.randint(0, self.timing[firstMutationPosition])
			self.timing[firstMutationPosition] = self.timing[firstMutationPosition] - decrement
			self.timing[secondMutationPosition] = self.timing[secondMutationPosition] + decrement

		#then it is done

	@classmethod
	def generateTrafficLightWithUpperAndLowerBound(cls, phaseNum, minimumTimeForEachPhase):
		timeList = []
		for _ in xrange(phaseNum):
			timeList.append(minimumTimeForEachPhase)
		for i in xrange(phaseNum):
			timeList[i] = timeList[i] + random.randint(0, cls.maxTime - minimumTimeForEachPhase)
		return timeList


