using System;
using System.Text;

namespace Decorator
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");

            MyStringBuilder builder = new MyStringBuilder();
            var str= builder.Append("test")
                .Append(true)
                .Append(1)
                .ToString();
        }
    }

    public class MyStringBuilder
    {
        private StringBuilder builder= new StringBuilder();

        public override string ToString()
        {
            return builder.ToString();
        }

        public MyStringBuilder Append(bool value)
        {
            //my logic
             builder.Append(value);
            return this;

        }
        public MyStringBuilder Append(string value)
        {
            builder.Append(value);
            return this;

        }
        public MyStringBuilder Append(byte value)
        {
             builder.Append(value);
             return this;


        }

        public MyStringBuilder Append(char value)
        {
             builder.Append(value);
             return this;

        }
        public MyStringBuilder Append(char value, int repeatCount)
        {
             builder.Append(value, repeatCount);
             return this;

        }

        public MyStringBuilder Append(char[]? value)
        {
             builder.Append(value);
             return this;

        }

        public MyStringBuilder Append(char[]? value, int startIndex, int charCount)
        {
             builder.Append(value, startIndex, charCount);
             return this;

        }
    }
}
