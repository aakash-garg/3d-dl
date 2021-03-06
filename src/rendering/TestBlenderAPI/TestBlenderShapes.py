import bpy

import sys

boop = '/Users/matthew/Documents/MSc/Group_Project/Lobster/src/'
if not (boop in sys.path):
    sys.path.append(boop)

C = bpy.context
C.scene.render.engine = 'CYCLES'


import unittest


from ..BlenderAPI.BlenderShapes import *

import os

class BlenderShapeTest(unittest.TestCase):

    def setUp(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()

    def tearDown(self):
        # delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()


    def test_cube_creation(self):
        # To pass the test these two conditions must be satisfied
        # I.e. Cube must not be present before, and must be present after
        no_cube_before = False
        cube_after = False

        # Check if cube is present before
        for obj in bpy.data.objects:
            if obj.name == "Cube":
                break
        else:
            no_cube_before = True

        # Create cube
        my_cube = BlenderCube()

        # Check if cube is present after
        for obj in bpy.data.objects:
            if obj.name == "Cube":
                cube_after = True
                break

        self.assertTrue(no_cube_before, "There was already a Cube before a cube was created!")
        self.assertTrue(cube_after, "There was no Cube even though it was supposed to have been created!")

    def test_plane_creation(self):
        # To pass the test these two conditions must be satisfied
        # I.e. Plane must not be present before, and must be present after
        no_plane_before = False
        plane_after = False

        # Check if plane is present before
        for obj in bpy.data.objects:
            if obj.name == "Plane":
                break
        else:
            no_plane_before = True

        # Create cube
        my_plane = BlenderPlane()

        # Check if cube is present after
        for obj in bpy.data.objects:
            if obj.name == "Plane":
                plane_after = True
                break

        self.assertTrue(no_plane_before, "There was already a Plane before a plane was created!")
        self.assertTrue(plane_after, "There was no Plane even though it was supposed to have been created!")

    def test_import_shape(self):
        test_dir = os.path.dirname(__file__)
        test_file_path = os.path.join(test_dir, 'test_files', 'example.obj')
        num_before = len(bpy.data.objects)
        cube = BlenderImportedShape(obj_path=test_file_path)
        num_after = len(bpy.data.objects)
        self.assertEqual(num_after - num_before, 1)

    def test_apply_texture(self):
        test_dir = os.path.dirname(__file__)
        test_file_path = os.path.join(test_dir, 'test_files', 'texture.jpg')
        my_cube = BlenderCube()
        success = my_cube.add_image_texture(test_file_path)
        self.assertTrue(success)

        success = my_cube.add_image_texture(test_file_path, mapping='Generated')
        self.assertTrue(success)

        success = my_cube.add_image_texture(test_file_path, mapping='Invalid')
        self.assertFalse(success)

        test_file_path = os.path.join(test_dir, 'test_files', 'texture_does_not_exist.jpg')
        success = my_cube.add_image_texture(test_file_path)
        self.assertFalse(success)

    def test_turn_on_off(self):

        my_cube = BlenderCube()
        my_cube_ref = bpy.data.objects[0]
        
        my_cube.turn_off()
        self.assertTrue(my_cube_ref.layers[1], "Object set to wrong layer")
        self.assertFalse(my_cube_ref.layers[0], "Object set to wrong layer")
        my_cube.turn_on()
        self.assertTrue(my_cube_ref.layers[0], "Object set to wrong layer")
        self.assertFalse(my_cube_ref.layers[1], "Object set to wrong layer")
        my_cube.turn_off()
        self.assertTrue(my_cube_ref.layers[1], "Object set to wrong layer")
        self.assertFalse(my_cube_ref.layers[0], "Object set to wrong layer")
        my_cube.turn_on()
        self.assertTrue(my_cube_ref.layers[0], "Object set to wrong layer")
        self.assertFalse(my_cube_ref.layers[1], "Object set to wrong layer")
        


if __name__ == '__main__':

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BlenderShapeTest)
    success = unittest.TextTestRunner().run(suite).wasSuccessful()

