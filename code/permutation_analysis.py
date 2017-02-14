from sklearn.base import clone
from multiprocessing import Pool
from sklearn.model_selection import train_test_split
import numpy as np

class Permutation(object):
	"""Permutation analysis suite for model evaluation.

	Keyword arguments:

	model -- the model estimator to be used in permutation test. Must have scikit-learn interface.
	features -- numpy array (or similar) of samples and features. 
	target   -- numpy array (or similar) of target response variable
	evaluator -- method with signature (model, features, target) --> score which evaluates the model
	given a set of features and targets. 
	test_size -- percentage of dataset to reserve for post-train testing in evaluator function.

	"""
	def __init__(self, model, features, target, evaluator, verbose=False):
		super(Permutation, self).__init__()
		self.model = model
		self.features = features
		self.target = target
		self.evaluator = evaluator
		self.verbose = verbose
		self._completed_tests = 0
		self.results = []


	def _permute_target(self):
		""" 
		Permutes target variables by selecting uniformly-distributed
		random values from within the domain of the target. Returns permuted target array.
		"""
		min = np.min(self.target)
		max = np.max(self.target)
		size = len(self.target)
		target_permuted = np.random.uniform(low=min,
											high=max,
											size=size)
		
		return target_permuted


	def benchmark(self):
		return self.evaluator(self.model, self.features, self.target)

	def _run_model(self, target):
		"""
		Runs model and returns output from evaluator function.
		"""
		## we have to do this to be threadsafe I think:
		thisModel = clone(self.model)
		## then run the model and save the result.
		result =  self.evaluator(thisModel, self.features, target)
		del thisModel
		if self.verbose: print (self._completed_tests, " completed.")
		self._completed_tests+=1
		return result


	def execute_test(self, n_tests=10, threads=10):
		"""
		Executes permutation test. 

		Keyword arguments:
		n_tests -- number of permutation trials. (default = 10)
		threads -- number of worker processes in threadpool. (default = 10)
		"""
		targets_permuted = [self._permute_target() for _ in range(0, n_tests)]

		threadPool = Pool(processes=threads)
		self.results = threadPool.map(self._run_model, targets_permuted)
		


