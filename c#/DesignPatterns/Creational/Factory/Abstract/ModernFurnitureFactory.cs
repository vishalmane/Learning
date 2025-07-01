namespace Factory.Method
{
    public class ModernFurnitureFactory : FurniturteFactory
    {
        public override Chair GetChair()
        {
            return new ModernChair();
        }

        public override Table GetTable()
        {
            return new ModernTable();
        }
    }
}
