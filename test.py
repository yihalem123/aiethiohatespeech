test_string = "https://www.facebook.com/312860729331033/posts/889372515013182/"
  
# printing original string 
print("The original string : " + test_string)
  
# using List comprehension + isdigit() +split()
# getting numbers from string 
res = [int(i) for i in test_string.split('/') if i.isdigit()]
  
# print result
print("The numbers list is : " + str(res))