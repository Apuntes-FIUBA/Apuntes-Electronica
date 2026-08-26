import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import sympy as sym
import sympy.printing as printing
import numpy as np
from IPython.display import display, Math
from ipywidgets import interact

class GraficaDeProceso:
    
    def __init__ (self,variablesStr,operacionesStr):        
        self.numVariables, self.numOperaciones = len(variablesStr), len(operacionesStr)
        self.variablesStr, self.operacionesStr = variablesStr, operacionesStr
        self.variables = sym.symbols(variablesStr)
        #self.toLatex('\\text{Variables de Entrada: }'+str(self.variables))         
        self.variables += sym.symbols('op:'+str(self.numOperaciones))
        self.Inherentes()
        self.Operaciones()       
        self.Factores()       
        self.Errores(0)       
        self.ErrorTotal(0)
        self.r = sym.symbols('r')
        self.mu = sym.symbols('mu')
    
    def toLatex(self,ec):
        display(Math(printing.latex(ec,mul_symbol='dot')))
        
    def Inherentes(self, view = 1):
        self.inherentes = []
        for variable in self.variables:
            self.inherentes.append(sym.symbols('i'+str(variable)))
        if (view): 
            self.toLatex('\\text{Errores Inherentes: }'+str(self.inherentes[:self.numVariables]))
        
    def Operaciones(self, view = 1):
        self.operaciones = []
        for operacionStr in self.operacionesStr:
            self.operaciones.append(sym.sympify(operacionStr))
        self.opSubs = self.operaciones[:]
        for i in range(0,self.numOperaciones):
            for j in range(0,i):        
                self.opSubs[i] = self.opSubs[i].subs('op'+str(j),self.opSubs[j])  
        if (view): 
            self.toLatex('\\text{Operaciones: }'+sym.printing.latex(self.opSubs,mul_symbol='dot'))                      
        self.redondeos = sym.symbols('mu:'+str(self.numOperaciones))
        
    def Factores(self, view = 0):
        self.factores = []   
        for i in range(0,self.numOperaciones):
            temp = []
            for j in range(0,self.numVariables+self.numOperaciones-1):
                factor = sym.diff(self.operaciones[i],self.variables[j])*self.variables[j]/self.operaciones[i]
                temp.append(factor)
            self.factores.append(temp)
        self.factoresSubs = self.factores[:][:]
        for k in range (0,len(self.factores)):
            for j in range (0,len(self.factores[k])):                  
                for i in range(0,self.numOperaciones):     
                        self.factoresSubs[k][j] = self.factoresSubs[k][j].subs('op'+str(i),self.opSubs[i])   
        if (view): 
            print('Factores de amplificación:')
            for op in self.factoresSubs:            
                self.toLatex(op)                                 

    def Errores(self, view = 1):
        self.errores = []
        for i in range(0,self.numVariables):
            self.errores.append(0)   
        for i in range(0,self.numOperaciones):
            self.errores.append(0)
            for j in range(0,self.numVariables+self.numOperaciones):
                factor = sym.diff(self.operaciones[i],self.variables[j])*self.variables[j]/self.operaciones[i]
                self.errores[i+self.numVariables] += factor * self.inherentes[j]
            self.errores[i+self.numVariables] += self.redondeos[i]
        self.numErrores = len(self.errores)
        if (view): 
            self.toLatex('Errores por operación:')
            for op in self.errores[self.numVariables:]:            
                self.toLatex(op)            


    def CpTeorico(self, view=1):
        self.problemaMatematico = self.opSubs[-1]
        self.cpTeorico = 0
        for variable in self.variables:
            self.cpTeorico += sym.Abs(sym.diff(self.problemaMatematico,variable)*variable/self.problemaMatematico)
        self.toLatex(self.cpTeorico)
                
    def CotaErrorTotal(self, view = 1):
        self.cota =  self.r*self.cp + self.mu*self.te
        if (view):
            self.toLatex('e_{total} \\leq' + sym.printing.latex(self.cota,mul_symbol='dot'))

    def ErrorTotal(self, view = 1):
        # Reemplazamos las operaciones por sus expresiones:
        for i in range(self.numVariables,self.numErrores):
            for j in range(self.numOperaciones+1,self.numVariables-1,-1):    
                self.errores[i] = self.errores[i].subs('op'+str(j-self.numVariables),self.operaciones[j-self.numVariables])
        # Reemplazamos los errores inherentes por sus expresiones:        
        for i in range(self.numVariables,self.numErrores):
            for j in range(self.numVariables,self.numErrores):    
                self.errores[i] = self.errores[i].subs(self.inherentes[j],self.errores[j])             
        self.errorTotal = self.errores[-1]
        self.errorTotal = sym.expand(self.errorTotal)
        self.errorTotal = sym.collect(self.errorTotal,self.inherentes)
        self.errorTotal = sym.collect(self.errorTotal,self.redondeos)     
        if (view):   
            self.toLatex('e_{total} = ' + sym.printing.latex(self.errorTotal,mul_symbol='dot'))              
            
    def Cp(self, simp = 0):
        if (simp):          
            self.toLatex(self.cp.simplify())   
        else:
            self.toLatex(self.cp)             

    def Te(self, simp = 0):
        if (simp):
            self.toLatex(self.te.simplify())   
        else:
            self.toLatex(self.te)                        
            
    def ErrorInherente(self, view = 1, r = False):
        self.errorInherente = self.errorTotal
        self.cp = 0
        for i in range(0,self.numOperaciones):
            self.errorInherente = self.errorInherente.subs(self.redondeos[i],0) 
        for i in range(0,self.numVariables):
            self.cp += sym.Abs(sym.diff(self.errorInherente,self.inherentes[i]))            
        self.funcionCp = sym.lambdify(self.variables[:self.numVariables], self.cp)   
        expr = self.errorInherente
        if (r):
            expr = self.r*self.cp
            expr = expr.expand()           
        if (view):   
            self.toLatex(expr)            
        
    def ErrorRedondeo(self, view = 1, mu = False):
        self.errorRedondeo = self.errorTotal
        self.te = 0
        for i in range(0,self.numVariables):
            self.errorRedondeo = self.errorRedondeo.subs(self.inherentes[i],0)
        for i in range(0,self.numOperaciones):
            self.te += sym.Abs(sym.diff(self.errorRedondeo,self.redondeos[i]))        
        expr = self.errorRedondeo
        if (mu): 
            expr = self.mu*self.te
            expr = expr.expand()                
        if (view):   
            self.toLatex(expr)           

    def GP(self, width=10, height=15, htext=(10,30), wrec=(1.0,15.0)):
        radio = 10
        vTgap = htext/4    
        vdist = 7*radio
        hdist = 5*radio

        fig=plt.figure(1, figsize=(width, height))
        ax=fig.add_subplot(1,1,1)
        xOp, yOp = [], []
        for i in range (0,self.numVariables+self.numOperaciones+1):
            xOp.append(0)
            yOp.append(0)
        #circle = plt.Circle((0, 0), radius=radio, ec='b', fc='none')

        texto = self.opSubs[-1]
        wRec = wrec*radio*len(str(texto))/8
        hRec = 2*radio
        circle = plt.Rectangle((-wRec/2, -hRec/2),wRec,hRec, ec='r', fc='none'  )    
        plt.text(0, 0, r'$'+printing.latex(texto,mul_symbol='dot')+'$',fontsize=htext, horizontalalignment='center', verticalalignment='center')  
        plt.text(wRec/2+5, 0, r'$'+printing.latex(self.redondeos[-1])+'$', size=htext, color='r')    
        ax.add_patch(circle)    
        #print(xOp,yOp)
        for op in range(self.numOperaciones-1,-1,-1):
            simbolos = self.operaciones[op].free_symbols
            #print ('Operacion',op,simbolos,len(simbolos))
            if (len(simbolos)==2):
                signo = 1
                hgap = radio
                vgap = radio
            else:
                signo = 0
                hgap = 0
                vgap = radio            
            for sim in simbolos:
                subOp = self.variables.index(sim)            
                if (subOp-self.numVariables>=0):
                    texto = self.opSubs[subOp-self.numVariables]
                else:
                    texto = self.variables[subOp]
                hTgap = htext*len(str(texto))/12
                if (len(str(texto))<6):
                    wRec = wrec*radio
                else:
                    wRec = wrec*radio*len(str(texto))/8
                hRec = 2*radio
                #print(printing.latex(texto))            
                xOp[subOp] = xOp[op+self.numVariables]+signo*hdist*(1+2*op/self.numOperaciones)
                yOp[subOp] = yOp[op+self.numVariables]+vdist*(1+op/self.numOperaciones)    
                #plt.text('middle','middle', '$'+str(self.variables[subOp])+'$',position=(xOp[subOp]-2, yOp[subOp]-1),size=htext)
                plt.text(xOp[subOp],yOp[subOp],r'$'+printing.latex(texto,mul_symbol='dot')+'$',fontsize=htext, horizontalalignment='center', verticalalignment='center')  
                #print([xOp[subOp], xOp[op]], [yOp[subOp], yOp[op]])
                line = mlines.Line2D([xOp[subOp], xOp[op+self.numVariables]+signo*hgap], [yOp[subOp]-radio, yOp[op+self.numVariables]+vgap], color='k', linestyle='-', linewidth=2)
                ax.add_line(line)            
                xFac = (xOp[subOp] + xOp[op+self.numVariables]+signo*hgap)/2 + radio
                yFac = (yOp[subOp]-radio + yOp[op+self.numVariables]+vgap)/2
                mult = printing.latex(self.factoresSubs[op][subOp]).count('frac')*0.5+1
                plt.text(xFac, yFac, r'$'+printing.latex(self.factoresSubs[op][subOp],mul_symbol='dot')+'$',size=mult*htext)
                if (subOp<self.numVariables):
                    circle = plt.Circle((xOp[subOp], yOp[subOp]), radius=radio, ec='g', fc='none')
                    plt.text(xOp[subOp]+radio+5, yOp[subOp], r'$'+printing.latex(self.inherentes[subOp])+'$',size=htext,color='g')                
                else:
                    circle = plt.Rectangle((xOp[subOp]-wRec/2, yOp[subOp]-hRec/2),wRec,hRec, ec='r', fc='none')   
                    plt.text(xOp[subOp]+wRec/2+5, yOp[subOp], r'$'+printing.latex(self.redondeos[subOp-self.numVariables])+'$',size=htext,color='r')                
                ax.add_patch(circle)   
                signo *= -1
                for linea in ax.spines: ax.spines[linea].set_visible(False)
                ax.set_yticks([])
                ax.set_xticks([])
        #print (xOp,yOp)
        plt.axis('scaled')
        plt.show()

    def mostrar(self, w=10, h=False, ht=False, wr=False):
        if (not h): h = w
        if (not ht): ht = (w, 5*w)
        if (not wr): wr = (1, 1.5*w)
        interact (self.GP, width=w, height=h, htext=ht, wrec=wr)

        