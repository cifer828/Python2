def is_prime(num):
  middle = num / 2 + 1
  for i in range(2, middle):
    if num % i == 0:
      return False
  return True

def output_prime(low_s, high_s):
  low = int(low_s)



