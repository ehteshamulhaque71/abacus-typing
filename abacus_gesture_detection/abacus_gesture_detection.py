import numpy as np
import math

class AbacusGesture():

	def transform_points(self, keypoints):
		x0 = keypoints[0][0]
		y0 = keypoints[0][1]
		x9 = keypoints[9][0]
		y9 = keypoints[9][1]
		a = math.degrees(math.atan2(y9 - y0, x9 - x0))
		a = (((a + 360) % 360) + 90) % 360
		a = math.radians(a)
		keypoints_transformed = self.transform(x0, y0, a, keypoints)
		return keypoints_transformed
	
	def transform(self, x, y, a, org):
		a = 2 * math.pi - a
		t = np.array([[1, 0, -x],
				[0, 1, -y],
				[0, 0, 1]])
		s = np.array([[1, 0, 0],
				[0, -1, 0],
				[0, 0, 1]])
		r = np.array([[np.cos(a), np.sin(a), 0],
				[-np.sin(a), np.cos(a), 0],
				[0, 0, 1]])
		return np.matmul(np.matmul(np.matmul(np.array(org), t.T), s.T), r.T)
          
	def calculateAbacusGesture(self, handLandmarks, handType):
		abacusGesture = 0
		multiplier = 10 if handType == 'left' else 1

		dist_thumb_tip = handLandmarks[4][0]
		dist_thumb_base = handLandmarks[3][0]
		checker = dist_thumb_tip * dist_thumb_base
		if checker < 0:
			pass
		elif abs(dist_thumb_tip) > abs(dist_thumb_base):
			abacusGesture += (5 * multiplier)
		dist_index_tip = abs(handLandmarks[8][1])
		dist_index_base = abs(handLandmarks[6][1])
		if dist_index_tip > dist_index_base:
			abacusGesture += (1 * multiplier)
		dist_middle_tip = abs(handLandmarks[12][1])
		dist_middle_base = abs(handLandmarks[10][1])
		if dist_middle_tip > dist_middle_base:
			abacusGesture += (1 * multiplier)
		dist_ring_tip = abs(handLandmarks[16][1])
		dist_ring_base = abs(handLandmarks[14][1])
		if dist_ring_tip > dist_ring_base:
			abacusGesture += (1 * multiplier)
		dist_pinky_tip = abs(handLandmarks[20][1])
		dist_pinky_base = abs(handLandmarks[18][1])
		if dist_pinky_tip > dist_pinky_base:
			abacusGesture += (1 * multiplier)
		return abacusGesture
	
	def getAbacusGesture(self, leftHandLandmarks, rightHandLandmarks, isLeftHand, isRightHand):
		leftSum, rightSum = 0, 0

		if isLeftHand:
			left_key_points_transformed = self.transform_points(leftHandLandmarks)
			leftSum = self.calculateAbacusGesture(left_key_points_transformed, 'left')

		if isRightHand:
			right_key_points_transformed = self.transform_points(rightHandLandmarks)
			rightSum = self.calculateAbacusGesture(right_key_points_transformed, 'right')

		return leftSum + rightSum