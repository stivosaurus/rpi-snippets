#!/usr/bin/env python

####


import math
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk # Python 3
####
  
class NthRootsGui(object):


  def __init__(self, n=36, winscale=0.43,
               backcol='#ffffff',
               col0='#ff0000', outline0='#000000',
               col1='#00ff00', outline1='#ffff00'):

    self.root = tk.Tk()
    self.root.title('nth roots & mouse check')
    self.col0 = col0
    self.col1 = col1
    self.outline0 = outline0
    self.outline1 = outline1

    scrsize = min(self.root.winfo_screenwidth(),
                  self.root.winfo_screenheight())
    canvsize = int(scrsize * winscale)
    self.canvas = tk.Canvas(self.root, bg=backcol,
                            width=canvsize, height=canvsize)
    
    self.slider = tk.Scale(self.root, from_=3, to=n,
                           orient=tk.HORIZONTAL,
                           command=self.show_roots)

    self.svar = tk.StringVar()
    self.lab = tk.Label(self.root, textvariable=self.svar,
                        font=('Monospace', 18, ''))
    self.canvas.bind('<Motion>', self.check_mouse)
    self.canvas.bind('<Configure>', self.resize)
    
    self.canvas.pack(fill=tk.BOTH, expand=True)
    self.slider.pack(fill=tk.X)
    self.lab.pack()

    self.canvas.after_idle(self.resize)

     
  def check_mouse(self, ev):

    canv = ev.widget
    mx, my = canv.canvasx(ev.x), canv.canvasy(ev.y)
    #self.svar.set('%s  %s' % (mx, my))
    self.highlight(*check_inout(mx, my, self.triangles))


  def highlight(self, nr, triangle):

    if nr < 0:
      self.svar.set('Mouse Outside')
      if self.last:
        self.canvas.create_polygon(self.last, fill=self.col0,
                                   outline=self.outline0)
        self.last = None
      return
    
    if not triangle == self.last:
      if self.last:
        self.canvas.create_polygon(self.last, fill=self.col0,
                                   outline=self.outline0)
      self.svar.set('Triangle: %3s' % nr)
      self.canvas.create_polygon(triangle, fill=self.col1,
                                 outline=self.outline1)
      self.last = triangle

    self.canvas.update_idletasks()

    
  def show_roots(self, *ev):

    self.triangles = make_roots(self.slider.get(),
                                self.center_x, self.center_y, self.scale)
    self.draw_triangles()

    
  def draw_triangles(self):
   
    self.canvas.delete('all')
    self.canvas.create_polygon(self.triangles, fill=self.col0,
                               outline=self.outline0)  
    self.canvas.update_idletasks()
    self.last = None

       
  def resize(self, *ev):

    w = self.canvas.winfo_width() - 1
    h = self.canvas.winfo_height() - 1
    self.center_x = w // 2
    self.center_y = h // 2
    self.scale = min(w-2, h-2) // 2
    self.show_roots()


  def run(self):

    self.root.mainloop()

####

def crossprod_sign(point, p0, p1):
  '''p0, p1 = line segment       
  '''
  px0, py0 = p0
  px1, py1 = p1
  vx, vy = point[0] - px0, point[1] - py0 
  wx, wy = px1 - px0, py1 - py0
  res = vx * wy - vy * wx
  
  if res > 0:
    return 1
  else:
    return -1

####
  
def make_roots(n, center_x, center_y, scale=1):

  delta = 2 * math.pi / n
    
  # with complex numbers:
  # z = complex(math.cos(delta), math.sin(delta))
  # poly = [z**i for i in xrange(n)]
  # points = map(lambda z: (z.real, z.imag), poly)
    
  points = [(math.cos(i * delta), math.sin(i * delta)) for i in xrange(n)]
  trans_points = [(center_x + scale * x,
                   center_y + scale * y) for x, y in points]
  
  return [((center_x, center_y), p1, p2) for p1, p2 in
          zip(trans_points, trans_points[1:] + [trans_points[0]])]

####

def check_inout(x, y, convex_polys):
    
  for i, points in enumerate(convex_polys):

    res = [crossprod_sign((x, y), p0, p1)
           for p0, p1 in zip(points, points[1:] + (points[0],))]
    #print res
    if set(res) == set([1]) or set(res) == set([-1]):
      return i, points

  return -1, None
  
####
    
if __name__ == '__main__':

  NthRootsGui(36).run()
