using System;

namespace Singleton
{
    class Program
    {
        static void Main(string[] args)
        {
            var connection = Connection.GetConnection();
            Console.WriteLine(Connection.index);
            var connection1 = Connection.GetConnection();
            Console.WriteLine(Connection.index);
            var connection2 = Connection.GetConnection();
            Console.WriteLine(Connection.index);
            var connection3 = Connection.GetConnection();
            Console.WriteLine(Connection.index);
            var connection4s = Connection.GetConnection();
            Console.ReadLine();
        }
    }
}
