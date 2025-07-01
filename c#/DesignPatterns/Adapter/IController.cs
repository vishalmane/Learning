namespace Adapter
{

    public interface IController
    {
        void RightBtnClick();
        void LetfBtnClick();
        void UpBtnClick();
        void DownBtnClick();
    }

    public abstract class PSController : IController
    {
        public abstract void DownBtnClick();
        public abstract void LetfBtnClick();
        public abstract void RightBtnClick();
        public abstract void UpBtnClick();
    }
    public abstract class XController : IController
    {
        public abstract void DownBtnClick();
        public abstract void LetfBtnClick();
        public abstract void RightBtnClick();
        public abstract void UpBtnClick();
    }


}
