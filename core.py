#!/usr/bin/python3

import tools

class EmpTerrain:
    def __init__(self, name, rgb, con_in, con_out):
        assert len(rgb) == 3, "3 times char is excpected"
        assert con_in>=0 and con_in<=1, "con_in out of range"
        assert con_out>=0 and con_out<=1, "con_out out of range"
        assert len(name)>=3 and len(name)<=14, "too long string"
        for c in rgb: 
            assert int(c)>=0 and int(c)<256, "3 chars are excpected"
        
        self.con_out = float(con_out)
        self.con_in = float(con_in)
        self.name = str(name)
        self.rgb = tuple(rgb)
        self.core = None

    def get_my_id(self):
        if self.core:
            for i,t in enumerate(self.core.terrains):
                if t.name == self.name: return i
            return -1
        else: return -1
                    
    def __repr__(self):
        k = self.get_my_id(), self.name, self.con_in, self.con_out, *self.rgb
        return "t%d:%s %g %g (%d,%d,%d)" % k
        
class EmpProvince:
    def __init__(self, name):
        assert len(name)>=3 and len(name)<=14, "too long string"
        self.name = str(name)
        self.core = None

    def get_my_id(self):
        if self.core:
            for i,p in enumerate(self.core.provinces):
                if p.name == self.name: return i
            return -1
        else: return -1
    
    def __repr__(self):
        return "p%d:%s" % (self.get_my_id(), self.name)

        
class EmpNation:
    def __init__(self, name):
        assert len(name)>=3 and len(name)<=14, "too long string"
        self.name = str(name)
        self.core = None

    def get_my_id(self):
        if self.core:
            for i,n in enumerate(self.core.nations):
                if n.name == self.name: return i
            return -1
        else: return -1

    def __repr__(self):
        return "n%d:%s" % (self.get_my_id(), self.name)

class EmpControl:
    def __init__(self, name):
        assert len(name)>=3 and len(name)<=14, "too long string"
        self.name = str(name)
        self.core = None

    def get_my_id(self):
        if self.core:
            for i,c in enumerate(self.core.controls):
                if c.name == self.name: return i
            return -1
        else: return -1

    def __repr__(self):
        return "c%d:%s" % (self.get_my_id(), self.name)

class EmpGood:
    def __init__(self, name):
        assert len(name)>=3 and len(name)<=14, "too long string"
        self.name = str(name)
        self.core = None

    def get_my_id(self):
        if self.core:
            for i,g in enumerate(self.core.goods):
                if g.name == self.name: return i
            return -1
        else: return -1

    def __repr__(self):
        return "g%d:%s" % (self.get_my_id(), self.name)

class EmpProcess:
    def __init__(self, name):
        assert len(name)>=3 and len(name)<=14, "too long string"
        self.name = str(name)
        self.core = None

    def get_my_id(self):
        if self.core:
            for i,x in enumerate(self.core.processes):
                if x.name == self.name: return i
            return -1
        else: return -1

    def __repr__(self):
        return "x%d:%s" % (self.get_my_id(), self.name)

class EmpAtom:
    def __init__(self, x, y, province, terrain):
        self.province = province
        self.terrain = terrain
        self.x,self.y = x,y

class EmpDiagram:
    def __init__(self, core, width, height):
        self.rgb = [0, 100, 100] * width * height
        self.atoms = [None] * width * height
        self.height = height
        self.width = width
        self.core = core

    def get_atom(self, x, y):
        tools.call_error(x<0 or y<0 or x>=self.width or y>=self.height, "out of diagram")
        return self.atoms[x+self.width*y]        
        
    def set_area(self, pixels, p, t):
        for x,y in pixels:
            if x<0 or y<0 or x>=self.width or y>=self.height: return

            i = 3*(x+self.width*y)
            self.rgb[i:i+2] = self.core.terrains[t].rgb[0:2]
            self.atoms[x+self.width*y] = EmpAtom(x, y, self.core.provinces[p], self.core.terrains[t])

    def set_border(self, pixel, p, t):
        atom = self.get_atom(*pixel)
        if atom == None: return
        if not atom.terrain is self.core.terrains[t]: return
        if not atom.province is self.core.provinces[p]: return
        checked = [False] * self.width * self.height
        to_check,to_change = [pixel],[]
        
        while to_check:
            xy = to_check.pop()
            checked[xy[0] + xy[1]*self.width] = True
            for x,y in [(0,1), (0,-1), (1,0), (-1,0)]:
                nxy = (xy[0]+x,xy[1]+y)
                if checked[nxy[0] + nxy[1]*self.width]: continue
                natom = self.get_atom(*nxy)
                if natom==None: to_change.append(nxy)
                elif not(atom.province is natom.province): to_change.append(nxy)
                elif not(atom.terrain is natom.terrain): to_change.append(nxy)
                else: to_check.append(nxy)
                
        self.set_area(to_change, p, t)
        
class EmpCore:
    def __init__(self, width, height):
        tools.call_error(width<10 or height<10, "width or height < 2")
        self.diagram = EmpDiagram(self, width, height)
        
        self.terrains = []
        self.provinces = []
        self.nations = []
        self.controls = []
        self.processes = []
        self.goods = []
        
    def add_terrain(self, name, rgb, con_in, con_out):
        try: nt = EmpTerrain(name, rgb, con_in, con_out)
        except AssertionError: return -1

        for t in self.terrains:
            if name==t.name: return -1
        nt.core = self
        self.terrains.append(nt)
        return len(self.terrains)-1 

    def rm_terrain(self, n):
        if n!=len(self.terrains)-1: return 1
        else: del self.terrains[n]
        return 0
    
    def add_province(self, name):
        try: np = EmpProvince(name)
        except AssertionError: return -1

        for p in self.provinces:
            if name==p.name: return -1
        np.core = self
        self.provinces.append(np)
        return len(self.provinces)-1 

    def rm_province(self, n):
        if n!=len(self.provinces)-1: return 1
        else: del self.provinces[n]
        return 0
    
    def add_nation(self, name):
        try: nn = EmpNation(name)
        except AssertionError: return -1

        for n in self.nations:
            if name==n.name: return -1
        nn.core = self
        self.nations.append(nn)
        return len(self.nations)-1 

    def rm_nation(self, n):
        if n!=len(self.nations)-1: return 1
        else: del self.nations[n]
        return 0
    
    def add_control(self, name):
        try: nc = EmpControl(name)
        except AssertionError: return -1

        for c in self.controls:
            if name==c.name: return -1
        nc.core = self
        self.controls.append(nc)
        return len(self.controls)-1 

    def rm_control(self, n):
        if n!=len(self.controls)-1: return 1
        else: del self.controls[n]
        return 0
    
    def add_good(self, name):
        try: ng = EmpGood(name)
        except AssertionError: return -1

        for g in self.goods:
            if name==g.name: return -1
        ng.core = self
        self.goods.append(ng)
        return len(self.goods)-1 

    def rm_good(self, n):
        if n!=len(self.goods)-1: return 1
        else: del self.goods[n]
        return 0
    
    def add_process(self, name):
        try: np = EmpProcess(name)
        except AssertionError: return -1

        for p in self.processes:
            if name==p.name: return -1
        np.core = self
        self.processes.append(np)
        return len(self.processes)-1
    
    def rm_process(self, n):
        if n!=len(self.processes)-1: return 1
        else: del self.processes[n]
        return 0