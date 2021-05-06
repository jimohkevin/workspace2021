ArrayList<float[]> points = new ArrayList<float[]>();
ArrayList<float[]> originalPoints = new ArrayList<float[]>();


//Transformation variable which uses linear matrix algebra
float transformation[][] = new float[][]{{1, 0, 0}, {0, -1, 0}, {0.75, 0, 0.25}};

void setup() {
  size(600, 600);

  background(255);

  //creates grid as points & stores them in arraylist

  //for (float i = -width*gridScale/2; i <= width*gridScale/2; i++) {
  //  for (float j = -height*gridScale/2; j <= height*gridScale/2; j++) {

  //      if (i%(width/num*gridScale) == 0) {
  //        float tempArray[] = new float[]{i, j};
  //        points.add(tempArray);
  //        originalPoints.add(tempArray);
  //      }
  //      if (j%(height/num*gridScale) == 0) {
  //        float tempArray[] = new float[]{i, j};
  //        points.add(tempArray);
  //        originalPoints.add(tempArray);
  //      }


  //  }
  //}
  
  //generates desired shape as points in a matrix
  for (float i = 0; i <= 10000; i++) {
    float tempArray[] = new float[]{cos(radians(i)), sin(radians(i)), asin(sin(i))};

    points.add(tempArray);
    originalPoints.add(tempArray);
  }

  //Displays original grid
  stroke(255, 0, 0);

  for (float[] point : originalPoints) {
    //point(point[0] + width/2, point[1] + height/2);
  }

  //modifies points

  for (float[] point : points) { 
    float mult = map(points.indexOf(point), 0, points.size(), 0, 600);

    point[0] *= mult/2;
    point[1] *= mult/2;
    point[2] *= mult/2;

    float p0 = point[0];
    float p1 = point[1];
    float p2 = point[2];
    
    
    
    point[0] = transformation[0][0] * p0 + transformation[1][0] * p1 + transformation[2][0] * p2;
    point[1] = transformation[0][1] * p0 + transformation[1][1] * p1 + transformation[2][1] * p2;
    point[2] = map(transformation[0][2] * p0 + transformation[1][2] * p1 + transformation[2][2] * p2, -mult/2, mult/2, 4, 0);

    println(point[2]);

    
  }

  //displays modified points
  stroke(0);


  for (float[] point : points) {

    //float zVal = map(point[2], -63, 63, 0.1, 5);
    color col = color(map(point[0], -width/2, width/2, 0, 255), map(point[1], -height/2, height/2, 0, 255), map(point[2], 5, 0.1, 0, 255));
    stroke(col);

    strokeWeight(point[2]);

    point(point[0] + width/2, point[1] + height/2);
  }
}

float zMax = 600;
int num = 25;
float gridScale = 0.5;
float depth = 10;

void draw() {
}
