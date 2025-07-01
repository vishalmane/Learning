namespace Factory.Method
{
    public abstract class Chair
    {
        public abstract void Legs();
        public abstract void Look();
    }

    public class MChair : Chair
    {
        public override void Legs()
        {
            throw new System.NotImplementedException();
        }

        public override void Look()
        {
            throw new System.NotImplementedException();
        }
    }
    public class CChair : Chair
    {
        public override void Legs()
        {
            throw new System.NotImplementedException();
        }

        public override void Look()
        {
            throw new System.NotImplementedException();
        }
    }
}
