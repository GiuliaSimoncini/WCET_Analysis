/*
  Bubble Sort Benchmark - Modified with Partially Ordered Input
  The array is initialized in sorted order, then a fraction
  of elements are randomly swapped to introduce disorder.
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
/* Fraction of pairs to swap (0.0 = fully sorted, 1.0 = fully shuffled) */
#define DISORDER_FRACTION 0.4

static int bsort_Array[ bsort_SIZE ];

/*
  Initialization- and return-value-related functions
*/

/*
  Initializes array in ascending order, then randomly swaps
  DISORDER_FRACTION of adjacent pairs to partially disorder it
*/
int bsort_Initialize( int Array[] )
{
  int Index, swaps, i, j, Temp;

  /* Fill with sorted values first */
  for ( Index = 0; Index < bsort_SIZE; Index++ )
    Array[Index] = Index * 10;

  /* Randomly swap a fraction of elements to introduce partial disorder */
  swaps = (int)( bsort_SIZE * DISORDER_FRACTION );
  for ( i = 0; i < swaps; i++ )
  {
    j = rand() % ( bsort_SIZE - 1 );
    Temp = Array[j];
    Array[j] = Array[j + 1];
    Array[j + 1] = Temp;
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
  srand((unsigned int)time(NULL));
  bsort_init();
  bsort_main();
  return bsort_return();
}