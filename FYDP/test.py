import unittest
import CSP as csp
import numpy as np

class CSPTests(unittest.TestCase):
	"""Unit tests for CSP module"""
	def testGenerateEMatrix(self):
		expected_matrix_1 = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
							[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
		expected_matrix_2 = [[0, 1, 2, 3],
							[0, 1, 2, 3],
							[0, 1, 2, 3],
							[0, 1, 2, 3],
							[0, 1, 2, 3],
							[0, 1, 2, 3],
							[0, 1, 2, 3],
							[0, 1, 2, 3],
							[0, 1, 2, 3],
							[0, 1, 2, 3],
							[0, 1, 2, 3],
							[0, 1, 2, 3],
							[0, 1, 2, 3],
							[0, 1, 2, 3]]
		channel_map_1 = {
			'r1':  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			'r2':  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			'r3':  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			'r4':  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			'r5':  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			'r6':  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			'r7':  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			'r8':  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			'r9':  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			'r10': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			'r11': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			'r12': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			'r13': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
			'r14': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        }
		channel_map_2 = {
            'r1':  [0, 1, 2, 3],
            'r2':  [0, 1, 2, 3],
            'r3':  [0, 1, 2, 3],
            'r4':  [0, 1, 2, 3],
            'r5':  [0, 1, 2, 3],
            'r6':  [0, 1, 2, 3],
            'r7':  [0, 1, 2, 3],
            'r8':  [0, 1, 2, 3],
            'r9':  [0, 1, 2, 3],
            'r10': [0, 1, 2, 3],
            'r11': [0, 1, 2, 3],
            'r12': [0, 1, 2, 3],
            'r13': [0, 1, 2, 3],
            'r14': [0, 1, 2, 3]
        }
		output_matrix_1 = csp.create_e_matrix(channel_map_1, 10)
		output_matrix_2 = csp.create_e_matrix(channel_map_2, 4)

		self.assertTrue(np.array_equal(output_matrix_1, expected_matrix_1))
		self.assertTrue(np.array_equal(output_matrix_2, expected_matrix_2))

	def testGenerateSignmaMatrix(self):
		#the number of rows should be 14
		
		e_matrix_array_input = [[[1,2,3],   [4,5,6],   [7,8,9]   ],
								[[10,11,12],[13,14,15],[16,17,18]],
								[[19,20,21],[22,23,24],[25,26,27]]
								]
		output_matrix = csp.generate_sigma_matrix(e_matrix_array_input, 3)
		expected_output_matrix = []
		self.assertTrue(output_matrix.matches(expected_output_matrix))
		
def main():
	unittest.main()

if __name__ == '__main__':
	main()