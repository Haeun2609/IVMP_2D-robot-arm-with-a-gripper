import pygame
import numpy as np

RED = (255, 0, 0)

FPS = 60   # frames per second

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def getRegularPolygon(nV, radius=1.):
    angle_step = 360. / nV 
    half_angle = angle_step / 2.

    vertices = []
    for k in range(nV):
        degree = angle_step * k 
        radian = np.deg2rad(degree + half_angle)
        x = radius * np.cos(radian)
        y = radius * np.sin(radian)
        vertices.append( [x, y] )
    #
    print("list:", vertices)

    vertices = np.array(vertices)
    print('np.arr:', vertices)
    return vertices


class myPolygon():
    def __init__(self, nvertices = 3, radius=70, color=(100,0,0), vel=[5.,0]):
        self.radius = radius
        self.nvertices = nvertices
        self.vertices = getRegularPolygon(self.nvertices, radius=self.radius)

        self.color = color
        self.color_org = color 

        self.angle = 0.
        self.angvel = np.random.normal(5., 7)

        self.position = np.array([0.,0]) #
        # self.position = self.vertices.sum(axis=0) # 2d array
        self.vel = np.array(vel)
        self.tick = 0

    def update(self,):
        self.tick += 1
        self.angle += self.angvel
        self.position += self.vel

        if self.position[0] >= WINDOW_WIDTH:
            self.vel[0] = -1. * self.vel[0]

        if self.position[0] < 0:
            self.vel[0] *= -1.

        if self.position[1] >= WINDOW_HEIGHT:
            self.vel[1] *= -1.

        if self.position[1] < 0:
            self.vel[1] *= -1

        # print(self.tick, self.position)

        return

    def draw(self, screen):
        R = Rmat(self.angle)
        points = self.vertices @ R.T + self.position

        pygame.draw.polygon(screen, self.color, points)
#

def update_list(alist):
    for a in alist:
        a.update()
#
def draw_list(alist, screen):
    for a in alist:
        a.draw(screen)
#

def Rmat(degree):
    rad = np.deg2rad(degree) 
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([ [c, -s, 0],
                   [s,  c, 0], [0,0,1]])
    return R

def Tmat(tx, ty):
    Translation = np.array( [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    return Translation
#

def draw(P, H, screen, color=(100, 200, 200)):
    R = H[:2,:2]
    T = H[:2, 2]
    Ptransformed = P @ R.T + T 
    pygame.draw.polygon(screen, color=color, 
                        points=Ptransformed)
    return
#


def main():
    pygame.init() # initialize the engine
    pygame.display.set_caption("20201174 Bui Ngoc Han")
    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    clock = pygame.time.Clock()

    w = 100
    h = 40
    X = np.array([ [0,0], [w, 0], [w, h], [0, h] ])
    gw = 60
    gh = 20
    G = np.array([ [0,0], [gw, 0], [gw, gh], [0, gh] ])
    dx = 0
    darm1 = 0
    darm2 = 0
    darm3 = 0
    gap = 0
    position = [WINDOW_WIDTH/2, WINDOW_HEIGHT - 100]
    base_x = 0
    arm1 = 0
    arm2 = 0
    arm3 = 0

    tick = 0
    done = False
    while not done:
        tick += 1
        #  input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_q:
                    darm1 = -1
                elif event.key == pygame.K_w:
                    darm1 = 1
                elif event.key == pygame.K_a:
                    darm2 = -1
                elif event.key == pygame.K_s:
                    darm2 = 1
                elif event.key == pygame.K_z:
                    darm3 = -1
                elif event.key == pygame.K_x:
                    darm3 = 1
                elif event.key == pygame.K_SPACE:
                    if (gap == -gw/2):
                        gap = 0
                    else: gap = -gw/2
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    dx = 0
                elif event.key == pygame.K_q or event.key == pygame.K_w:
                    darm1 = 0
                elif event.key == pygame.K_a or event.key == pygame.K_s:
                    darm2 = 0
                elif event.key == pygame.K_z or event.key == pygame.K_x:
                    darm3 = 0
                # elif event.key == pygame.K_SPACE:
                #     gap = 0

        # drawing
        screen.fill( (202, 240, 248))
        arm1 += darm1
        arm2 += darm2
        arm3 += darm3
        base_x += dx

        # base
        H0 = Tmat(position[0]-w/2, position[1]) @ Tmat(base_x, -h)
        draw(X, H0, screen, (3, 4, 94)) # base

        # arm 1
        H1 = H0 @ Tmat(w/2, 0)  
        H11 = H1 @ Rmat(-90) @ Tmat(0,-h/2)
        H12 = H11 @ Tmat(0, h/2) @ Rmat(arm1) @ Tmat(0, -h/2)    
        draw(X, H12, screen, (2, 62, 138)) #arm1

        # arm 2
        H2 = H12 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 2
        H21 = H2 @ Rmat(arm2) @ Tmat(0, -h/2)
        draw(X, H21, screen, (0, 119, 182)) #arm 2

        #arm 3
        H3 = H21 @ Tmat(w, 0) @ Tmat(0, h/2) #joint 3
        H32 = H3 @ Rmat(arm3) @ Tmat(0, -h/2)
        draw(X, H32, screen,(0, 150, 199)) #arm 3

        #grip
        G1 = H32 @ Tmat(w+gh*2, 0) @ Tmat(0, h/2)
        G11 = G1 @ Rmat(90) @ Tmat(-gw/2, gh)
        draw(G, G11, screen,(0, 180, 216))
        G2 = G11 @ Tmat(gw,0) @ Tmat(0, gh/2)
        G21 = G2 @ Rmat(90) @ Tmat(-gw, -gh - gap)
        draw(G, G21, screen, (0, 180, 216))
        G3 = G11 @ Tmat(gw,0) @ Tmat(0, gh/2)
        G31 = G3 @ Rmat(90) @ Tmat(-gw, 3*gh + gap)
        draw(G, G31, screen, (0, 180, 216))

    
        # pygame.draw.circle(screen, RED, (cx, cy), radius=3)
        # finish
        pygame.display.flip()
        clock.tick(FPS)
    # end of while
# end of main()

if __name__ == "__main__":
    main()