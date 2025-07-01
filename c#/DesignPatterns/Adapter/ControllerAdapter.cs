namespace Adapter
{
    public class ControllerAdapter : PSController
    {
        public XController outController { get; set; }

        public ControllerAdapter()
        {
            outController = new XBoxController();            
        }      

        public override void DownBtnClick()
        {
            outController.DownBtnClick();
        }

        public override void LetfBtnClick()
        {
            outController.LetfBtnClick();
        }

        public override void RightBtnClick()
        {
            outController.RightBtnClick();
        }

        public override void UpBtnClick()
        {
            outController.UpBtnClick();
        }
    }


}
