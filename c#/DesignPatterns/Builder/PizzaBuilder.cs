namespace Builder
{

    class Margherita : PizzaBuilder
    {
        public Margherita(Size size = Size.Large)
        {
            Size = size;
        }

        internal override PizzaBuilder AddCheese(Cheese cheese = Cheese.Mozzarella)
        {
            Cheese = cheese;
            return this;
        }

        internal override PizzaBuilder AddSauce()
        {
            return this;
        }

        internal override PizzaBuilder AddPepperoni()
        {
            return this;
        }

        internal override PizzaBuilder AddHam()
        {
            return this;

        }

        internal override PizzaBuilder AddOlives()
        {
          
            return this;
        }

        internal override PizzaBuilder AddMushrooms()
        {
            return this;
        }        
    }

    class FarmHouse : PizzaBuilder
    {
        public FarmHouse(Size size = Size.Large)
        {
            Size = size;
        }

        internal override PizzaBuilder AddCheese(Cheese cheese)
        {
            throw new System.NotImplementedException();
        }

        internal override PizzaBuilder AddHam()
        {
            throw new System.NotImplementedException();
        }

        internal override PizzaBuilder AddMushrooms()
        {
            throw new System.NotImplementedException();
        }

        internal override PizzaBuilder AddOlives()
        {
            throw new System.NotImplementedException();
        }

        internal override PizzaBuilder AddPepperoni()
        {
            throw new System.NotImplementedException();
        }

        internal override PizzaBuilder AddSauce()
        {
            throw new System.NotImplementedException();
        }
    }

    abstract class PizzaBuilder
    {
        public Size Size { get; set; }
        public Cheese Cheese { get; set; }
        public bool Sauce { get; set; }
        public bool Pepperoni { get; set; }
        public bool Ham { get; set; }
        public bool Olives { get; set; }
        public bool Mushrooms { get; set; }

        public Pizza Build()
        {
            return new Pizza(this);
        }
        internal abstract PizzaBuilder AddCheese(Cheese cheese);
        internal abstract PizzaBuilder AddSauce();
        internal abstract PizzaBuilder AddPepperoni();
        internal abstract PizzaBuilder AddHam();
        internal abstract PizzaBuilder AddOlives();
        internal abstract PizzaBuilder AddMushrooms();
    }
}
