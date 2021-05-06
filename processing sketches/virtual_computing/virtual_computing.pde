int data;
int numX = 1, numY = 1;

void setup() {
  size(400, 400);

  background(255);

  strokeWeight(2);
  stroke(0);

  point(width/2, height/2);
  
  for (int i = 0; i <= width*height; i++) {
    int x = i%width;
    int y = i - i%width;

    color c = get(x, y);

    if (c == color(0)) {
      println(x + ", " + y + true);
    }

    println(x + ", " + y);
  }
}

void draw() {
  
}

void mouseClicked() {
  setup();
}
