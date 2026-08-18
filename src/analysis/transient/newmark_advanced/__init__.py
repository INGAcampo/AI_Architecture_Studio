class NewmarkAdvancedEngine:
    def step(self,u,v,a,force,mass,damping,stiffness,dt,beta=.25,gamma=.5):
        ke=stiffness+gamma*damping/(beta*dt)+mass/(beta*dt*dt)
        pe=force+mass*(u/(beta*dt*dt)+v/(beta*dt)+(1/(2*beta)-1)*a)
        un=pe/max(ke,1e-12)
        an=(un-u)/(beta*dt*dt)-v/(beta*dt)-(1/(2*beta)-1)*a
        vn=v+dt*((1-gamma)*a+gamma*an)
        return un,vn,an
