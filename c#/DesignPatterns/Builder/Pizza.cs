namespace Builder
{
    public enum Cheese { Cheddar, Mozzarella, Parmesan, Provolone }
    public enum Size { Small, Medium, Large, XLarge }
    class Pizza
    {
        public Size Size { get; set; }
        public Cheese Cheese { get; set; }
        public bool Sauce { get; set; }
        public bool Pepperoni { get; set; }
        public bool Ham { get; set; }
        public bool Olives { get; set; }
        public bool Mushrooms { get; set; }

        public Pizza(PizzaBuilder builder)
        {
            Size = builder.Size;
            Cheese = builder.Cheese;
            Sauce = builder.Sauce;
            Pepperoni = builder.Pepperoni;
            Ham = builder.Ham;
            Olives = builder.Olives;
            Mushrooms = builder.Mushrooms;
        }
        
    }
}
