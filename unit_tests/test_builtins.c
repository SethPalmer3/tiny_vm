/* Test cases for builtins.{c,h} */
#include "../builtins.h"
#include <assert.h>
#include <stdlib.h>

extern obj_ref int_literal(char *n);

void test_Int() {
  obj_ref i = new_int(42);
  // obj_ref i = int_literal("42");
  assert(i->fields);
}

int main(int argc, char *argv[]) {
  test_Int();

  return EXIT_SUCCESS;
}
