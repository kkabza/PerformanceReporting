USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_AuctionResults]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_AuctionResults](
	[SaleId] [int] IDENTITY(1,1) NOT NULL,
	[QueueId] [int] NOT NULL,
	[PropertyNo] [varchar](50) NOT NULL,
	[TaxYear] [int] NOT NULL,
	[VGProductID] [int] NOT NULL,
	[MinimumBid] [decimal](18, 2) NOT NULL,
	[NumberOfBidders] [int] NOT NULL,
	[WinningBid] [decimal](18, 2) NOT NULL,
	[UnpaidBalance] [money] NOT NULL,
	[UserID] [uniqueidentifier] NOT NULL,
	[BidderNumber] [varchar](4) NULL,
	[SequenceNo] [int] NULL,
 CONSTRAINT [PK_vg_AuctionResults] PRIMARY KEY CLUSTERED 
(
	[SaleId] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
