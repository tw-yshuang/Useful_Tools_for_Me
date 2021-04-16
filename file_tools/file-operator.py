
def replace_keyword(filename, target_word, replace_word):
  new_f = ''
  with open(filename, 'r') as f:
    new_f = f.read().replace(target_word, replace_word)
  with open(filename, 'w') as f:
    f.write(new_f)

def find_keyword(filename, keyword):
  keyword_set = set()
  
  with open(filename, 'r') as f:
    for line in f.readlines():
      keyword_index = line.find(keyword)
      if keyword_index != -1:
        keyword_set.add(line[keyword_index+len(keyword):])

  return list(sorted(keyword_set))

def main():
  pass

if __name__ == "__main__":
  main()
