namespace Factory.Method
{
    public class ClassicFurnitureFactory : FurniturteFactory
    {
        public override Chair GetChair()
        {
            return new ClassicChair();
        }

        public override Table GetTable()
        {
            return new ClassicTable();
        }
    }
}
