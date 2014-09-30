import itertools
import os
from PIL import Image
from PIL import ImageDraw


IMAGE_SIZE=32

def make_file_name(sequence):
  base = ','.join([str(s) for s in sequence])
  return  os.path.join('images', base+'.png')


def draw_board(sequence):
  image = Image.new('RGBA', (IMAGE_SIZE,IMAGE_SIZE))
  draw = ImageDraw.Draw(image)
  
  third = IMAGE_SIZE/3
  offset = third/4

  # first draw the lines
  draw.line((third,0,third,IMAGE_SIZE), fill='white')
  draw.line((2*third,0,2*third,IMAGE_SIZE), fill='white')
  draw.line((0, third,IMAGE_SIZE, third), fill='white')
  draw.line((0, 2*third,IMAGE_SIZE,2*third), fill='white')

  # now add the pices on the board
  for i in xrange(9):
    x = i % 3
    y = i / 3
    move = sequence[i]
    if move == 1:
      x = x * third
      y = y * third
      # draw an here
      draw.line((x+offset,y+offset,x+third-offset,y+third-offset), fill='red')
      draw.line((x+third-offset,y+offset,x+offset,y+third-offset), fill='red')
    elif move == -1:
      x = x * third
      y = y * third
      draw.arc((x+offset,y+offset,x+third-offset,y+third-offset),0, 360, fill='green')

  image.save(make_file_name(sequence))
      

base_board = [0 for x in xrange(9)]

def copy_board(board):
  return [ b for b in board]

def next_turn_boards(board, is_x_turn):
  for i, move in itertools.izip(xrange(9), board): 
    if move == 0:
      new_board = copy_board(board)
      new_board[i] =  1 if is_x_turn else -1 
      yield new_board

def make_images_for_turns(boards, n_turns=3):
  to_process = []
  is_x_turn = n_turns % 2 == 1
  for base_board in boards: 
    for new_board in next_turn_boards(base_board, is_x_turn):
      draw_board(new_board)
      to_process.append(new_board)
  if n_turns > 0:
    print ('new level with %d roots' % len(to_process) )
    make_images_for_turns(to_process, n_turns-1)
    


def main():
  draw_board([1,0,0,1,0,0,0,-1,0])

if __name__ == '__main__' : main()
