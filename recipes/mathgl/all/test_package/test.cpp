#include <cstdlib>
#include <iostream>
#include "mgl2/mgl.h"

int main() {

  mglGraph mg;
  mg.Alpha(true);
  return EXIT_SUCCESS;
}


// #include <mgl2/qt.h>
// int sample(mglGraph *gr)
// {
//   gr->Rotate(60,40);
//   gr->Box();
//   return 0;
// }
// //-----------------------------------------------------
// int main(int argc,char **argv)
// {
//   mglQT gr(sample,"MathGL examples");
//   return gr.Run();
// }
