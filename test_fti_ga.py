from fixed_time_interval_ga import FixedTimeIntervalGA
import random
if __name__ == "__main__":

	#the total length of the region is 800 steps
	#it means that we divide the whole interval into 4 sub-regions
	#we have 10 individuals as a population
	simulationStep = 600
	intervalNum = 4
	instance = FixedTimeIntervalGA(intervalNum, simulationStep, 20, 6)
	bestIndividual = None
	bestFitness = -0x7FFFFFF

	maximumGenerationNum = 10 
	random.seed(101)#prev was 10
	#10 - 157
	currentBestOutput = open("currentBest" + str(maximumGenerationNum) + ".txt", "w")
	currentMeanOutput = open("currentMean" + str(maximumGenerationNum) + ".txt", "w")
	

	instance.generateIndividualList()

	for i in xrange(maximumGenerationNum):
		instance.generateOffspring()
		instance.mutate()
		instance.evaluateAll()
		instance.rank()
		currentBest = instance.getBestIndividual()	
		currentBestOutput.write(str(currentBest.fitness) + "\n")
		currentMeanOutput.write(str(instance.getAverageFitness()) + "\n")
		print(currentBest.fitness)
		if(currentBest.fitness > bestFitness):
			bestIndividual = currentBest
			bestFitness = currentBest.fitness
		instance.select()
	currentBestOutput.close()
	currentMeanOutput.close()
	
	
	bestOutput = open("best" + str(maximumGenerationNum) + ".txt", "w")
	for i in xrange(intervalNum):
		bestOutput.write(str(bestIndividual.genes[i].timing) + "\n")
		bestOutput.write(str(bestFitness))
	bestOutput.close()
	print bestFitness
	





