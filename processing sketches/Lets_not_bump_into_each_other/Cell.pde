public class Cell {
  PVector pos;
  PVector vel = new PVector(0, 0);
  PVector accel = new PVector(0, 0);
  
  PVector drag = new PVector(0, 0);
  PVector gravity = new PVector(0, 1).normalize();
  
  int s;
  
  color col;
  
  public Cell(PVector pos, int s){
     this.pos = pos;
     this.s = s;
     
     this.col = color(random(255), random(255), random(255));
     
  }
  
  public void display(){
    fill(this.col);
    ellipse(this.pos.x, this.pos.y, this.s, this.s);
  }
  
  public void update(int xBounds[], int yBounds[]){
    this.pos.add(this.vel);
    this.vel.add(this.accel);
    this.accel.set(0, 0);
    
    this.keepInBounds(xBounds, yBounds);
    this.drag = this.vel.copy().mult(1/2*1.225*0.47*width*height);
    //this.airFriction.normalize();
  }
  
  public void applyForce(PVector force){
    this.accel = force;
  }
  
  public void keepInBounds(int xBounds[], int yBounds[]){
    float friction = 0.98;
    
    if(this.pos.x < xBounds[0] + this.s/2){
      this.vel.x *= -friction;
      this.pos.x = xBounds[0] + this.s/2;
    }
    
    if(this.pos.x > xBounds[1] - this.s/2){
      this.vel.x *= -friction;
      this.pos.x = xBounds[1] - this.s/2;
    }
    
    if(this.pos.y < yBounds[0] + this.s/2){
      this.vel.y *= -friction;
      this.pos.y = yBounds[0] + this.s/2;
    }
    
    if(this.pos.y > yBounds[1] - this.s/2){
      this.vel.y *= -friction;
      this.pos.y = yBounds[1] - this.s/2;
    }
  }
  
  
}
