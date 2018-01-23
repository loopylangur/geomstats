"""Unit tests for hyperbolic_space module."""

import math
import numpy as np
import unittest

from geomstats.hyperbolic_space import HyperbolicSpace


class TestHyperbolicSpaceMethods(unittest.TestCase):
    DIMENSION = 6
    SPACE = HyperbolicSpace(dimension=DIMENSION)
    METRIC = SPACE.metric

    def test_random_uniform_and_belongs(self):
        """
        Test that the random uniform method samples
        on the hyperbolic space.
        """
        point = self.SPACE.random_uniform()
        self.assertTrue(self.SPACE.belongs(point))

    def test_intrinsic_and_extrinsic_coords(self):
        """
        Test that the composition of
        intrinsic_to_extrinsic_coords and
        extrinsic_to_intrinsic_coords
        gives the identity.
        """
        point_int = np.ones(self.DIMENSION)
        point_ext = self.SPACE.intrinsic_to_extrinsic_coords(point_int)
        result = self.SPACE.extrinsic_to_intrinsic_coords(point_ext)
        expected = point_int

        self.assertTrue(np.allclose(result, expected))

        point_ext = self.SPACE.random_uniform()
        point_int = self.SPACE.extrinsic_to_intrinsic_coords(point_ext)
        result = self.SPACE.intrinsic_to_extrinsic_coords(point_int)
        expected = point_ext

        self.assertTrue(np.allclose(result, expected))

        self.assertTrue(np.allclose(result, expected))

    def test_log_and_exp_general_case(self):
        """
        Test that the riemannian exponential
        and the riemannian logarithm are inverse.

        Expect their composition to give the identity function.
        """
        # Riemannian Log then Riemannian Exp
        # General case
        base_point_1 = self.SPACE.random_uniform()
        point_1 = self.SPACE.random_uniform()

        log_1 = self.METRIC.log(point=point_1, base_point=base_point_1)
        result_1 = self.METRIC.exp(tangent_vec=log_1, base_point=base_point_1)
        expected_1 = point_1

        self.assertTrue(np.allclose(result_1, expected_1))

    def test_squared_norm_and_squared_dist(self):
        """
        Test that the squqred distance between two points is
        the squared norm of their logarithm.
        """
        point_a = self.SPACE.random_uniform()
        point_b = self.SPACE.random_uniform()
        log = self.METRIC.log(point=point_a, base_point=point_b)
        result = self.METRIC.squared_norm(vector=log)
        expected = self.METRIC.squared_dist(point_a, point_b)

        self.assertTrue(np.allclose(result, expected))

    def test_norm_and_dist(self):
        """
        Test that the distance between two points is
        the norm of their logarithm.
        """
        point_a = self.SPACE.random_uniform()
        point_b = self.SPACE.random_uniform()
        log = self.METRIC.log(point=point_a, base_point=point_b)
        result = self.METRIC.norm(vector=log)
        expected = self.METRIC.dist(point_a, point_b)

        self.assertTrue(np.allclose(result, expected))

    def test_log_and_exp_edge_case(self):
        """
        Test that the riemannian exponential
        and the riemannian logarithm are inverse.

        Expect their composition to give the identity function.
        """
        # Riemannian Log then Riemannian Exp
        # Edge case: two very close points, base_point_2 and point_2,
        # form an angle < epsilon
        base_point_intrinsic_2 = np.array([1., 2., 3., 4., 5., 6.])
        base_point_2 = self.SPACE.intrinsic_to_extrinsic_coords(
                                                       base_point_intrinsic_2)
        point_intrinsic_2 = (base_point_intrinsic_2
                             + 1e-12 * np.array([-1., -2., 1., 1., 2., 1.]))
        point_2 = self.SPACE.intrinsic_to_extrinsic_coords(
                                                       point_intrinsic_2)

        log_2 = self.METRIC.log(point=point_2, base_point=base_point_2)
        result_2 = self.METRIC.exp(tangent_vec=log_2, base_point=base_point_2)
        expected_2 = point_2

        self.assertTrue(np.allclose(result_2, expected_2))

    def test_exp_and_log_and_projection_to_tangent_space_general_case(self):
        """
        Test that the riemannian exponential
        and the riemannian logarithm are inverse.

        Expect their composition to give the identity function.
        """
        # Riemannian Exp then Riemannian Log
        # General case
        base_point_1 = self.SPACE.random_uniform()
        # TODO(nina): this fails for high euclidean norms of vector_1
        vector_1 = np.array([9., 4., 0., 0., -1., -3., 2.])
        vector_1 = self.SPACE.projection_to_tangent_space(
                                                  vector=vector_1,
                                                  base_point=base_point_1)
        exp_1 = self.METRIC.exp(tangent_vec=vector_1, base_point=base_point_1)
        result_1 = self.METRIC.log(point=exp_1, base_point=base_point_1)

        expected_1 = vector_1
        self.assertTrue(np.allclose(result_1, expected_1))

    def test_exp_and_log_and_projection_to_tangent_space_edge_case(self):
        """
        Test that the riemannian exponential
        and the riemannian logarithm are inverse.

        Expect their composition to give the identity function.
        """
        # Riemannian Exp then Riemannian Log
        # Edge case: tangent vector has norm < epsilon
        base_point_2 = self.SPACE.random_uniform()
        vector_2 = 1e-10 * np.array([.06, -51., 6., 5., 6., 6., 6.])

        exp_2 = self.METRIC.exp(tangent_vec=vector_2, base_point=base_point_2)
        result_2 = self.METRIC.log(point=exp_2, base_point=base_point_2)
        expected_2 = self.SPACE.projection_to_tangent_space(
                                                   vector=vector_2,
                                                   base_point=base_point_2)

        self.assertTrue(np.allclose(result_2, expected_2))

    def test_dist(self):
        # Distance between a point and itself is 0.
        point_a_1 = self.SPACE.random_uniform()
        point_b_1 = point_a_1
        result_1 = self.METRIC.dist(point_a_1, point_b_1)
        expected_1 = 0.

        self.assertTrue(np.allclose(result_1, expected_1))

    def test_exp_and_dist_and_projection_to_tangent_space(self):
        # TODO(nina): this fails for high norms of vector_1
        base_point_1 = self.SPACE.random_uniform()
        vector_1 = np.array([2., 0., -1., -2., 7., 4., 1.])
        tangent_vec_1 = self.SPACE.projection_to_tangent_space(
                                                vector=vector_1,
                                                base_point=base_point_1)
        exp_1 = self.METRIC.exp(tangent_vec=tangent_vec_1,
                                base_point=base_point_1)

        result_1 = self.METRIC.dist(base_point_1, exp_1)
        sq_norm = self.METRIC.embedding_metric.squared_norm(
                                                 tangent_vec_1)
        expected_1 = math.sqrt(sq_norm)
        self.assertTrue(np.allclose(result_1, expected_1))

    def test_variance(self):
        point = self.SPACE.random_uniform()
        result = self.METRIC.variance([point, point])
        expected = 0

        self.assertTrue(np.allclose(result, expected))

    def test_mean(self):
        point = self.SPACE.random_uniform()
        result = self.METRIC.mean([point, point])
        expected = point

        self.assertTrue(np.allclose(result, expected))

    def test_mean_and_belongs(self):
        point_a = self.SPACE.random_uniform()
        point_b = self.SPACE.random_uniform()
        point_c = self.SPACE.random_uniform()

        result = self.METRIC.mean([point_a, point_b, point_c])
        self.assertTrue(self.SPACE.belongs(result))


if __name__ == '__main__':
        unittest.main()