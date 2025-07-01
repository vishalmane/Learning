using System;
using System.Text;

namespace Builder
{
    class Program
    {
        static void Main(string[] args)
        {
            
            Console.WriteLine("Hello World!");
            var margheritaPizza = new Margherita(Size.Medium)
                .AddCheese()
                .AddSauce()
                .Build();
            var farmHousePizza = new FarmHouse(Size.Small)
                .AddSauce()
                .AddCheese(Cheese.Mozzarella)
                .AddHam()
                .AddMushrooms()
                .AddOlives()
                .AddPepperoni()
                .AddSauce()
                .Build();                    
        }
    }

   

}
