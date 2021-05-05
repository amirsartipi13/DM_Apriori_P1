

library(arules)
dataset = read.csv('Project1-groceries.csv', header = FALSE)
dataset = read.transactions('Project1-groceries.csv', sep = ',', rm.duplicates = TRUE)
summary(dataset)



rules = apriori(data = dataset, parameter = list(support= 0.005, confidence=0.6))


inspect(sort(rules, by='lift'))

