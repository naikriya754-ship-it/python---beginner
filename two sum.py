#Input: nums = [2,7,11,15], target = 9
#Output: [0,1]
#num = [3,2,4] , target = 6
#num = [3,3]  , target = 6
class Solution:
    def twosum(nums , target):
        for i in range(len(nums)):
            for j in range(i+1,len(nums)):
                if nums[i] + nums[j] == target:
                   return [i,j]
