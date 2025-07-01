using System;

namespace Memento
{

    // // The Memento design pattern without violating encapsulation, 
    // captures and externalizes an object‘s internal state 
    // so that the object can be restored to this state later. 
    class Program
    {
        static void Main(string[] args)
        {
            Memento Memento= new Memento();
            TextEditer txEditer = new TextEditer();
            Console.WriteLine(txEditer.Text);
            txEditer.Text = "Hi Vishal";
            Memento.Save(txEditer.Text);
            Console.WriteLine(txEditer.Text);

            txEditer.Text = "Hi Sachin";
            Memento.Save(txEditer.Text);
            Console.WriteLine(txEditer.Text);
            
            txEditer.Text = "Hi Sachin and Vishal";
            Memento.Save(txEditer.Text);
            Console.WriteLine(txEditer.Text);

            txEditer.Text = Memento.UnDo();
            Console.WriteLine($"UnDo 1:{txEditer.Text}");
            
            txEditer.Text = Memento.UnDo();
            Console.WriteLine($"UnDo 2:{txEditer.Text}");


            txEditer.Text = Memento.UnDo();
            Console.WriteLine($"UnDo 3:{txEditer.Text}");


            txEditer.Text = Memento.ReDo();
            Console.WriteLine($"ReDo 1:{txEditer.Text}");


            txEditer.Text = Memento.ReDo();
            Console.WriteLine($"ReDo 2:{txEditer.Text}");


           


            Console.ReadLine();

        }
    }
}
