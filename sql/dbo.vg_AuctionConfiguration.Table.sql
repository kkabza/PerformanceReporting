USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_AuctionConfiguration]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_AuctionConfiguration](
	[AuctionId] [int] NOT NULL,
	[AuctionName] [varchar](50) NOT NULL,
	[AuctionStartDate] [datetime] NOT NULL,
	[BiddingType] [int] NOT NULL,
	[AuctionType] [int] NOT NULL,
	[BidIncrement] [decimal](18, 2) NOT NULL,
	[MaximumBid] [decimal](18, 2) NOT NULL,
	[MinimumBid] [decimal](18, 2) NOT NULL,
	[AuctionActive] [bit] NOT NULL,
	[AuctionDeleted] [bit] NOT NULL,
	[NumberOfQueues] [int] NULL,
	[AuctionValue] [money] NULL,
	[VGProductId] [int] NOT NULL
) ON [PRIMARY]
GO
