using System;

namespace Template
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
        }
    }

    public abstract class BookProcess
    {
        public abstract void SearchProduct();
        public abstract void ComparePrice();
        public abstract void CheckRevires();
        public abstract void AddToCart();
        public abstract void CheckoutCart();
        public abstract void MakePayment();

        public void BookProduct()
        {
            SearchProduct();
            ComparePrice();
            CheckRevires();
            AddToCart();
            CheckoutCart();
            MakePayment();
        }
    }
    public class Amazone:BookProcess
    {
        public override void SearchProduct()
        {
            
        }

        public override void ComparePrice()
        {
        }

        public override void CheckRevires()
        {
        }

        public override void AddToCart()
        {
        }

        public override void CheckoutCart()
        {
        }

        public override void MakePayment()
        {
        }
    }
    public class Flipcart:BookProcess
    {
        public override void SearchProduct()
        {
            
        }

        public override void ComparePrice()
        {
        }

        public override void CheckRevires()
        {
        }

        public override void AddToCart()
        {
        }

        public override void CheckoutCart()
        {
        }

        public override void MakePayment()
        {
        }
    }
}
