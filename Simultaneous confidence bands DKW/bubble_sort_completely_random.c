/*
  Bubble Sort Benchmark - Modified with Random Input
*/

#include <stdlib.h>
#include <time.h>

/*
  Forward declaration of functions
*/

void bsort_init( void );
void bsort_main( void );
int bsort_return( void );
int bsort_Initialize( int Array[] );
int bsort_BubbleSort( int Array[] );


/*
  Declaration of global variables
*/

#define bsort_SIZE 1000

static int bsort_Array[ bsort_SIZE ];


/*
  Initialization- and return-value-related functions
*/

/* Initializes given array with randomly generated integers */
int bsort_Initialize( int Array[] )
{
  int Index;

  _Pragma( "loopbound min 1000 max 1000" )
  for ( Index = 0; Index < bsort_SIZE; Index++ )
  {
    /* Random numbers between -1000 and 1000 */
    Array[Index] = (rand() % 2001) - 1000;
  }

  return 0;
}


void bsort_init( void )
{
  bsort_Initialize( bsort_Array );
}


int bsort_return( void )
{
  int Sorted = 1;
  int Index;

  _Pragma( "loopbound min 999 max 999" )
  for ( Index = 0; Index < bsort_SIZE - 1; Index++ )
    Sorted = Sorted && ( bsort_Array[Index] <= bsort_Array[Index + 1] );

  return 1 - Sorted;
}


/*
  Core benchmark functions
*/

/* Sorts an array of integers of size bsort_SIZE in ascending
   order with bubble sort. */
int bsort_BubbleSort( int Array[] )
{
  int Sorted = 0;
  int Temp, Index, i;

  for ( i = 0; i < bsort_SIZE - 1; i++ )
  {
    Sorted = 1;
    for ( Index = 0; Index < bsort_SIZE - i - 1; Index++ )
    {
      if ( Array[Index] > Array[Index + 1] )
      {
        Temp = Array[Index];
        Array[Index] = Array[Index + 1];
        Array[Index + 1] = Temp;
        Sorted = 0;
      }
    }

    if ( Sorted )
      break;
  }

  return 0;
}


void _Pragma( "entrypoint" ) bsort_main( void )
{
  bsort_BubbleSort( bsort_Array );
}


/*
  Main function
*/

int main( void )
{
  /* Seed random generator once */
  srand((unsigned int)time(NULL));

  bsort_init();
  bsort_main();

  return bsort_return();
}
