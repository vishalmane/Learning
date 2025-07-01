using Factory.Factory;
using Factory.Method;
using System;

namespace Factory
{
    class Program
    {
        static void Main(string[] args)
        {
            

            //Simple Factory
            var fileLogger = LogFactory.CreateLogger(LogType.File);
            var dbLogger = LogFactory.CreateLogger(LogType.SQL);

            //Abstract Factory
            ClientCode modern = new ClientCode(new ModernFurnitureFactory());
            ClientCode classic = new ClientCode(new ClassicFurnitureFactory());



        }
    }



    class ClientCode
    {
        readonly FurniturteFactory furniturteFactory;

        public ClientCode(FurniturteFactory furniturteFactory)
        {
            this.furniturteFactory = furniturteFactory;
        }
        public void OrderFurniture()
        {
            furniturteFactory.GetChair();
            furniturteFactory.GetTable();
        }
    }



}
