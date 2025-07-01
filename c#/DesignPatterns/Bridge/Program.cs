using System;

namespace Bridge
{
    class Program
    {
        static void Main(string[] args)
        {
           new Good.A4Page(new Good.Dotmatrix()).PrintJob();
            new Bad.A4SizePageDM().PrintJob();
        }
    }

   


}
